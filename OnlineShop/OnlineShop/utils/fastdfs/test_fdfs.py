from fdfs_client.client import Fdfs_client

client = Fdfs_client(r"client.conf文件路径")
ret = client.upload_by_filename("图片路径")
client.download_to_file("file nam", "Remote file_id")
