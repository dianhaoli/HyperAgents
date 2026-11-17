"""Symlink/FIFO/hardlink-safe file access for root operating on agent-controlled paths.

Rule: root never follows a link, never opens a non-regular file, never runs git, and never writes through a
path inside an agent-writable tree. All agent processes are dead (their pid namespace is gone) before
any of these functions runs on their files, so there is no concurrent mutation (no TOCTOU).
"""
import io
import os
import shutil
import stat
import tarfile

SKIP_DIRS = {".git", "__pycache__"}


def safe_read_bytes(path, max_bytes=50_000_000):
    """Bytes of a regular, single-link, non-symlink file; None otherwise."""
    try:
        st = os.lstat(path)
    except OSError:
        return None
    if not stat.S_ISREG(st.st_mode) or st.st_nlink != 1 or st.st_size > max_bytes:
        return None
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    except OSError:
        return None
    try:
        st2 = os.fstat(fd)
        if (st2.st_ino, st2.st_dev) != (st.st_ino, st.st_dev) or not stat.S_ISREG(st2.st_mode):
            return None
        with os.fdopen(fd, "rb", closefd=False) as f:
            return f.read(max_bytes)
    finally:
        os.close(fd)


def safe_read_text(path, max_bytes=50_000_000):
    b = safe_read_bytes(path, max_bytes)
    return None if b is None else b.decode("utf-8", errors="replace")


def _is_real_dir(p):
    try:
        return stat.S_ISDIR(os.lstat(p).st_mode)
    except OSError:
        return False


def inside(path, base):
    """True if path's components (no symlink resolution of the final link) stay under base and no
    component on the way is a symlink."""
    base = os.path.realpath(base)
    p = os.path.abspath(path)
    if not (p == base or p.startswith(base + os.sep)):
        return False
    cur = base
    for comp in os.path.relpath(p, base).split(os.sep):
        if comp in ("", "."):
            continue
        cur = os.path.join(cur, comp)
        try:
            if stat.S_ISLNK(os.lstat(cur).st_mode):
                return False
        except FileNotFoundError:
            return True
    return True


def safe_copytree(src, dst, base, skip_dirs=SKIP_DIRS):
    """Copy only regular files / real dirs from agent-controlled `src` (must be inside `base`, no symlinked
    components) into root-controlled `dst`. Returns list of skipped entries."""
    skipped = []
    if not inside(src, base) or not _is_real_dir(src):
        raise ValueError(f"unsafe source {src}")
    os.makedirs(dst, exist_ok=True)
    for root, dirs, files in os.walk(src, followlinks=False):
        rel = os.path.relpath(root, src)
        keep = []
        for d in dirs:
            if d in skip_dirs:
                continue
            if _is_real_dir(os.path.join(root, d)):
                keep.append(d)
            else:
                skipped.append(os.path.join(rel, d))
        dirs[:] = keep
        od = os.path.join(dst, rel) if rel != "." else dst
        os.makedirs(od, exist_ok=True)
        for fn in files:
            b = safe_read_bytes(os.path.join(root, fn))
            if b is None:
                skipped.append(os.path.join(rel, fn))
                continue
            with open(os.path.join(od, fn), "wb") as f:
                f.write(b)
    return skipped


def safe_copyfile(src, dst, base):
    if not inside(src, base):
        raise ValueError(f"unsafe source {src}")
    b = safe_read_bytes(src)
    if b is None:
        raise ValueError(f"not a regular file: {src}")
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, "wb") as f:
        f.write(b)


def snapshot_tree(src, tar_path, base):
    """tar.gz of the regular files of an agent tree (no .git, no __pycache__, no links)."""
    if not inside(src, base) or not _is_real_dir(src):
        raise ValueError(f"unsafe source {src}")
    os.makedirs(os.path.dirname(tar_path), exist_ok=True)
    tmp = tar_path + ".tmp"
    skipped = []
    with tarfile.open(tmp, "w:gz") as tar:
        for root, dirs, files in os.walk(src, followlinks=False):
            dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and _is_real_dir(os.path.join(root, d)))
            for fn in sorted(files):
                p = os.path.join(root, fn)
                b = safe_read_bytes(p)
                if b is None:
                    skipped.append(os.path.relpath(p, src))
                    continue
                ti = tarfile.TarInfo(os.path.relpath(p, src))
                ti.size = len(b)
                ti.mode = 0o644
                tar.addfile(ti, io.BytesIO(b))
    os.replace(tmp, tar_path)
    return skipped


def extract_snapshot(tar_path, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.makedirs(dest)
    with tarfile.open(tar_path, "r:gz") as tar:
        for m in tar.getmembers():
            if not m.isfile() or m.name.startswith("/") or ".." in m.name.split("/"):
                continue
            out = os.path.join(dest, m.name)
            os.makedirs(os.path.dirname(out), exist_ok=True)
            with open(out, "wb") as f:
                f.write(tar.extractfile(m).read())
    return dest


def lchown_tree(path, uid, gid):
    for root, dirs, files in os.walk(path, followlinks=False):
        os.lchown(root, uid, gid)
        for n in dirs + files:
            try:
                os.lchown(os.path.join(root, n), uid, gid)
            except FileNotFoundError:
                pass
