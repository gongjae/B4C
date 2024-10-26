import struct

def parse_ntfs(file_path):
    with open(file_path, 'rb') as f:
        print("# GPT (MBR)\n")
        
        # MBR에서 GPT
        f.seek(446)
        boot_indicator = struct.unpack("<B", f.read(1))[0]
        f.read(7)
        lba_start_address = struct.unpack("<I", f.read(4))[0]
        total_sectors = struct.unpack("<I", f.read(4))[0]
        print(f"@ GPT(MBR) - Partition table entry")
        print(f"Boot Indicator:  {boot_indicator}")
        print(f"LBA Start Address:  {lba_start_address} sector")
        print(f"Total Sector :  0x{total_sectors:08x}")
        
        # GPT Header
        f.seek(512)  
        gpt_header = f.read(92)  # GPT 헤더 전체를 읽기 위해 92바이트
        signature = gpt_header[:8]
        print(f"\n@ GPT (MBR) - GPT Header")
        print(f"Signature:  {signature.decode('utf-8')}")
        
        backup_lba = struct.unpack("<Q", gpt_header[32:40])[0]
        print(f"Backup LBA:  {backup_lba}")
        
        partition_start_lba = struct.unpack("<Q", gpt_header[40:48])[0]
        print(f"Starting LBA for partition:  {partition_start_lba} sector")
        
        partition_end_lba = struct.unpack("<Q", gpt_header[48:56])[0]
        print(f"Ending LBA for partition:  {partition_end_lba} sector")
        
        num_partition_entries = struct.unpack("<I", gpt_header[80:84])[0]
        size_of_partition_entry = struct.unpack("<I", gpt_header[84:88])[0]
        print(f"Number of partition entries:  {num_partition_entries}")
        print(f"Size of each entry:  {size_of_partition_entry}")
        
        print("\n@ GPT (MBR) - GPT Partition Entry\n")

        total_partitions = 0  # 유효한 파티션 개수를 카운트할 변수

        # 각 파티션 엔트리 읽기
        for i in range(num_partition_entries):
            # 각 엔트리의 시작 오프셋 계산
            entry_offset = 512 + size_of_partition_entry * i
            
            f.seek(entry_offset)  # 해당 엔트리로 이동
            partition_type_guid = f.read(16)  # 파티션 타입 GUID
            unique_partition_guid = f.read(16)  # 유니크 파티션 GUID
            starting_lba = struct.unpack("<Q", f.read(8))[0]  # 시작 LBA
            ending_lba = struct.unpack("<Q", f.read(8))[0]  # 종료 LBA
            attribute_flags = f.read(8)  # 속성 플래그
            partition_name = f.read(72)  # 파티션 이름
            
            # 파티션 이름을 UTF-16LE로 디코딩
            partition_name_str = partition_name.decode('utf-16le').rstrip('\x00')
            partition_size_mb = (ending_lba - starting_lba + 1) * 512 / (1024 * 1024)  # MB로 변환
            
            # 파티션 정보 출력: 데이터가 있는 경우에만 출력
            if starting_lba < ending_lba:  # 유효한 LBA 범위 확인
                total_partitions += 1  # 유효한 파티션 개수 증가
                print(f"- Partition {total_partitions}")
                print(f"Partition start offset: {starting_lba} sector")
                print(f"Partition end offset: {ending_lba} sector")
                print(f"Partition Size: {partition_size_mb:.2f}MB")
                print(f"Partition attribute(flag): {' '.join(attribute_flags.hex()[i:i+2] for i in range(0, len(attribute_flags.hex()), 2))}")
                print(f"Partition Name: {partition_name_str}\n")

                # Basic Data Partition인 경우 VBR과 MFT 정보를 읽음
                if partition_name_str == "Basic data partition":
                    # VBR 읽기
                    vbr_offset = starting_lba * 512  # VBR의 시작 오프셋
                    f.seek(vbr_offset)  # VBR로 이동
                    
                    jump_boot_code = f.read(3)  # 점프 부트 코드
                    oem_id = f.read(8)  # OEM ID
                    bytes_per_sector = struct.unpack("<H", f.read(2))[0]  # 섹터당 바이트 수
                    sectors_per_cluster = struct.unpack("<B", f.read(1))[0]  # 클러스터당 섹터 수
                    start_cluster_mft = struct.unpack("<Q", f.read(8))[0]  # $MFT의 시작 클러스터
                    start_cluster_mftmirr = struct.unpack("<Q", f.read(8))[0]  # $MFTMirr의 시작 클러스터

                    print(f"# VBR (Only {partition_name_str})")
                    print(f"Jump Boot Code: {' '.join(jump_boot_code.hex()[i:i+2] for i in range(0, len(jump_boot_code.hex()), 2))}")
                    print(f"OEM ID (str/hex): {oem_id.decode('ascii').strip()} / {' '.join(oem_id.hex()[i:i+2] for i in range(0, len(oem_id.hex()), 2))}")
                    print(f"Bytes Per Sector: {bytes_per_sector}")
                    print(f"Sectors Per Cluster: {sectors_per_cluster}")
                    print(f"Start Cluster for $MFT: {start_cluster_mft}")
                    print(f"Start Cluster for $MFTMirr: {start_cluster_mftmirr}")

                    # MFT 정보 출력
                    mft_start_offset = (starting_lba + start_cluster_mft * sectors_per_cluster)  # MFT 시작 오프셋 계산
                    print(f"\n# MFT (Master File Table)")
                    print(f"MFT Start offset: {mft_start_offset} sector\n")

        # 총 파티션 개수 출력
        print(f"총 파티션 개수: {total_partitions}")

# 실행
parse_ntfs(".\\NTFS.001")
