import unicodedata
import re

# Function to remove diacritics from a string
def remove_diacritics(s):
    if not isinstance(s, str):
        raise TypeError('Expected a string')
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

# Function to convert a string into a URL-friendly slug
def vietnamese_title(slug):
    # Đổi ký tự có dấu thành không dấu
    slug = re.sub(r'á|à|ả|ạ|ã|ă|ắ|ằ|ẳ|ẵ|ặ|â|ấ|ầ|ẩ|ẫ|ậ', 'a', slug, flags=re.IGNORECASE)
    slug = re.sub(r'é|è|ẻ|ẽ|ẹ|ê|ế|ề|ể|ễ|ệ', 'e', slug, flags=re.IGNORECASE)
    slug = re.sub(r'i|í|ì|ỉ|ĩ|ị', 'i', slug, flags=re.IGNORECASE)
    slug = re.sub(r'ó|ò|ỏ|õ|ọ|ô|ố|ồ|ổ|ỗ|ộ|ơ|ớ|ờ|ở|ỡ|ợ', 'o', slug, flags=re.IGNORECASE)
    slug = re.sub(r'ú|ù|ủ|ũ|ụ|ư|ứ|ừ|ử|ữ|ự', 'u', slug, flags=re.IGNORECASE)
    slug = re.sub(r'ý|ỳ|ỷ|ỹ|ỵ', 'y', slug, flags=re.IGNORECASE)
    slug = re.sub(r'đ', 'd', slug, flags=re.IGNORECASE)
    # Xóa các ký tự đặc biệt
    slug = re.sub(r'[\`~!@#\|\$%\^&\*\(\)\+=,\.\/\?\>\<\'\":;_]', '', slug)
    return slug

def slugify(s):
    return vietnamese_title(s) \
        .lower() \
        .strip() \
        .replace(' ', '-') \
        .replace('--', '-')

# Example usage
# print(slugify("Đây là một tiêu đề bài viết!"))