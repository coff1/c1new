import magic

def extract_file_suffix_in_url(url):
    # Split the URL by '/' to get the last part (the file name)
    file_name = url.split('/')[-1]
    
    # Split the file name by '?' to remove any URL parameters
    file_name = file_name.split('?')[0]
    
    # Split the file name by '.' to get the suffix
    suffix = file_name.split('.')[-1]
    
    # 排除提取到域名后缀的可能
    if len(file_name.split('.'))<2 or ':' in suffix or suffix in ["com", "org", "net", "edu", "gov", "mil", "int", "ac", "ad", "ae", "af", "ag", "ai", "al", "am", "ao", "aq", "ar", "as", "at", "au", "aw", "ax", "az", "ba", "bb", "bd", "be", "bf", "bg", "bh", "bi", "bj", "bm", "bn", "bo", "br", "bs", "bt", "bv", "bw", "by", "bz", "ca", "cc", "cd", "cf", "cg", "ch", "ci", "ck", "cl", "cm", "cn", "co", "cr", "cu", "cv", "cw", "cx", "cy", "cz", "de", "dj", "dk", "dm", "do", "dz", "ec", "ee", "eg", "er", "es", "et", "eu"]:
        suffix = ""
    # if suffix not in ["html","js","php","jsp","jspx","css"]:
    #     suffix = ""
    return "-"+suffix

def determine_file_type_with_content(content):
    # Use the magic library to determine the file type of the content
    file_type = magic.from_buffer(content, mime=True)
    return file_type

def determine_file_type_to_natural_language(content,url):
    file_type_with_content=determine_file_type_with_content(content)
    type = "unknow"

    if "text" in file_type_with_content:
        type = "text"+ extract_file_suffix_in_url(url)

    if "image" in file_type_with_content:
        type = "image" + extract_file_suffix_in_url(url)

    if "audio" in file_type_with_content:
        type = "audio" + extract_file_suffix_in_url(url)

    if "video" in file_type_with_content:
        type = "video" + extract_file_suffix_in_url(url)

    # 文档文件
    if file_type_with_content in ["application/msword"]:
        type = "document-doc" 
    if file_type_with_content in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        type = "document-docx" 
    if file_type_with_content in ["application/pdf"]:
        type = "document-pdf" 
    # xlsx和xls放一块因为能由一个函数提取内容
    if file_type_with_content in ["application/vnd.ms-excel","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
        type = "document-excel" 

    # 压缩/打包文件
    if file_type_with_content in ["application/zip","application/x-rar","application/x-7z","application/x-gzip","application/x-bzip2"]:
        type = "Compressed file" 

    return type