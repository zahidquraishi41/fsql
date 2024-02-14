image_ext = ('jpeg', 'png', 'gif', 'bmp', 'tiff', 'raw', 'psd', 'svg', 'ico', 'heic', 'webp', 'cr2', 'nef', 'arw', 'dng', 'jpg', 'tif', 'heif')
video_extensions = ('mp4', 'mkv', 'avi', 'mov', 'wmv', 'flv', 'webm', 'mpeg', 'mpg', '3gp', 'm4v', 'rm', 'swf', 'vob', 'ogg', 'm2ts', 'mts', 'ts', 'f4v', 'divx', 'rmvb', 'asf')
audio_extensions = ('mp3', 'wav', 'flac', 'aac', 'ogg', 'wma', 'm4a', 'opus', 'aiff', 'mid', 'midi', 'amr', 'ac3', 'mka')
application_extensions = ('exe', 'msi', 'apk', 'app', 'jar', 'bat', 'com', 'cmd', 'sh', 'deb', 'dmg', 'rpm')
document_extensions = ('pdf', 'doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx', 'odt', 'odp', 'ods', 'txt', 'rtf', 'csv', 'html', 'xml')
compressed_extensions = ("zip", "rar", "7z", "tar", "gz", "bz2", "xz", "z")
font_extensions = ("ttf", "otf", "woff", "woff2")
archive_extensions = ("tar", "gz", "bz2", "xz", "zip", "rar", "7z")
code_extensions = ("py", "java", "cpp", "c", "html", "css", "js", "php", "rb")
known_types = ('image', 'video', 'audio', 'application', 'document', 'compressed', 'font', 'archive', 'code', 'all')


def get_file_type(extension: str) -> str:
    if extension.startswith('.'):
        extension = extension[1:]
    if extension in image_ext:
        return 'image'
    if extension in video_extensions:
        return 'video'
    if extension in audio_extensions:
        return 'audio'
    if extension in application_extensions:
        return 'application'
    if extension in document_extensions:
        return 'document'
    if extension in compressed_extensions:
        return 'compressed'
    if extension in font_extensions:
        return 'font'
    if extension in archive_extensions:
        return 'archive'
    if extension in code_extensions:
        return 'code'

    return 'file'
