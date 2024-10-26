import zipfile
import struct
import os

def parse_zip(zip_file_path, output_file_path):
    
    with open(output_file_path, 'w', encoding='utf-8') as f:
        # zip 파일을 읽기 모드로 오픈
        with zipfile.ZipFile(zip_file_path, 'r') as zipf:
            # End of Central Directory Record 파싱 
            f.write("# End of central directory record\n")
            with open(zip_file_path, 'rb') as zf:
                # End of Central Directory Record -> zip 파일 끝에서 22바이트에 위치
                zf.seek(-22, 2)  # 파일 끝에서 22바이트 전으로 이동
                eocd_data = zf.read(22)  # 22바이트 읽음
                # 읽은 데이터 언팩
                signature, disk_num, disk_with_cd, disk_entries, total_entries, cd_size, cd_offset = struct.unpack('<4s4H2L', eocd_data[:20])
                # <는 리틀 엔디언으로, 4s는 4바이트 문자열(시그니처) 4H는 8바이트, 2L은 8바이트
                comment_len = struct.unpack('<H', eocd_data[20:22])[0]  # 마지막 2바이트는 코멘트 길이
                
                # End of Central Directory Record에 해당하는 정보 출력
                f.write(f"File signature (Magic Number): {signature.hex().upper()} \n")
                f.write(f"Disk Start Number: {disk_num}\n")
                f.write(f"Disk # w/cd: {disk_with_cd}\n")
                f.write(f"Disk Entry: {disk_entries}\n")
                f.write(f"Total Entry: {total_entries}\n")
                f.write(f"Size of Central Directory: {cd_size}\n")
                f.write(f"Central Header Offset: {cd_offset}\n")
                f.write(f"Comment Length: {'None' if comment_len == 0 else comment_len}\n")
                f.write("\n----------------------------------------------------------\n\n")

            # Central Directory File Headers 파싱
            f.write("# Central Directory File header\n")
            for i, zinfo in enumerate(zipf.infolist()):
                # 각 파일의 중앙 디렉토리 헤더 정보를 기록
                f.write(f"\n#{i}. Central Directory File header\n")
                f.write(f"File signature (Magic Number): 50 4B 01 02 \n")
                f.write(f"Version made by: {zinfo.create_version >> 8}\n") 
                f.write(f"Version needed to extract (minimum): {zinfo.extract_version}\n")
                f.write(f"Flags: {zinfo.flag_bits}\n")
                f.write(f"Compression method: {zinfo.compress_type}\n")  
                f.write(f"Moditime/Modidate: {zinfo.date_time[3] * 256 + zinfo.date_time[4]}/{zinfo.date_time[0] * 512 + zinfo.date_time[1]}\n")  # 수정 시간 및 날짜
                f.write(f"CRC-32 CheckSum: {zinfo.CRC}\n") 
                f.write(f"Compressed Size/Uncompressed Size: {zinfo.compress_size}/{zinfo.file_size}\n")
                f.write(f"File Name Length/Extra Field Length: {len(zinfo.filename)}/{len(zinfo.extra)}\n")
                f.write(f"File Comment Length: {len(zinfo.comment)}\n")
                f.write(f"Disk Start Number: {zinfo.volume}\n")
                f.write(f"Internal Attribute: {zinfo.internal_attr}\n")
                f.write(f"External Attribute: {zinfo.external_attr}\n")
                f.write(f"Local Header: {zinfo.header_offset}\n")
                f.write(f"File Name: {zinfo.filename}\n")
                f.write("\n----------------------------------------------------------\n")

            # Local File Headers 파싱
            f.write("\n# Local File Header\n")
            for i, zinfo in enumerate(zipf.infolist()):
                # 각 파일의 로컬 파일 헤더 정보 기록
                f.write(f"\n#{i}. Local File Header\n")
                f.write(f"File signature (Magic Number): 50 4B 03 04\n")  # 파일 시그니처
                f.write(f"Version needed to extract: {zinfo.extract_version}\n")
                f.write(f"Flags: {zinfo.flag_bits}\n")
                f.write(f"Compression method: {zinfo.compress_type}\n")
                f.write(f"Moditime/Modidate: {zinfo.date_time[3] * 256 + zinfo.date_time[4]}/{zinfo.date_time[0] * 512 + zinfo.date_time[1]}\n")
                f.write(f"CRC-32 CheckSum: {zinfo.CRC}\n")
                f.write(f"Compressed Size/Uncompressed Size: {zinfo.compress_size}/{zinfo.file_size}\n")
                f.write(f"File Name Length/Extra Field Length: {len(zinfo.filename)}/{len(zinfo.extra)}\n")
                f.write(f"File Name: {zinfo.filename}\n")

#파일 경로 설정
zip_file_path = './png.zip'
output_file_path = './output.txt'

# 함수 실행
parse_zip(zip_file_path, output_file_path)
