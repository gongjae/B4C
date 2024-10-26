import struct

def parsing(file_path):
    with open(file_path, 'rb') as f:
        
        print("# MBR\n")
        print(f"@ Partition 0")
        f.read(446)  # MBR의 첫 446바이트를 읽어옴
            
        # Boot Flag
        bootFlag = f.read(1)
        print("Boot Flag: 0x" + bootFlag.hex())
            
        # CHS Addr (Starting)
        chs_addr = f.read(3)
        print("Starting CHS Addr: 0x" + chs_addr.hex())
        
        # Part Type
        part_type = f.read(1)
        print("Part Type: 0x" + part_type.hex())
        
        # CHS Addr (Ending)
        end_chs_addr = f.read(3)
        print("Ending CHS Addr: 0x" + end_chs_addr.hex())
        
        # Starting LBA Addr
        starting_lba_addr = f.read(4)
        starting_lba_value = struct.unpack("<I", starting_lba_addr)[0]
        print(f"Starting LBA Addr: {starting_lba_value} sector")
        
        # Size in Sectors
        size_in_sectors = struct.unpack("<I", f.read(4))[0]
        print(f"Size in Sector: {size_in_sectors}")
        
        print("\n-----MBR Check Complete-----\n")
        
        # Reserved Area and Boot Sector Info
        f.seek(starting_lba_value * 512)  # LBA 주소를 바이트로 변환해 이동
        print(f"@ Partition: 0")
        print("# Reserved Area")
        print(f"sector: {starting_lba_value}")
        
        # Jump Boot Code
        jump_boot_code = f.read(3)
        print("Jump Boot Code: " + ' '.join(f"{byte:02x}" for byte in jump_boot_code))
        
        # OEM ID
        oem_id = f.read(8)
        print(f"OEM ID: {oem_id.decode('ascii')} / {' '.join(f'{byte:02x}' for byte in oem_id)}")
        
        # Bytes Per Sector
        bytes_per_sector = struct.unpack("<H", f.read(2))[0]
        print(f"Bytes Per Sector: {bytes_per_sector}")
        
        # Sectors Per Cluster
        sectors_per_cluster = struct.unpack("<B", f.read(1))[0]
        print(f"Sectors Per Cluster: {sectors_per_cluster}")
        
        # Reserved Sector Count
        reserved_sector_count = struct.unpack("<H", f.read(2))[0]
        print(f"Reserved Sector Count: {reserved_sector_count}")
        
        # FAT32 Size
        f.seek(11, 1)  
        fat_size = struct.unpack("<I", f.read(4))[0]
        print(f"FAT32 Size: {fat_size} sectors")
        
        # FAT Area Calculation
        fat_area_start = starting_lba_value + reserved_sector_count
        print(f"\n# FAT Area")
        print(f"sector (FAT Area #1): {fat_area_start}")
        
        # Backup FAT Area Calculation
        # FAT#2 starts right after FAT#1, so we add `fat_size` (in sectors).
        backup_fat_area_start = fat_area_start + fat_size
        print(f"Backup FAT Area (FAT Area #2): {backup_fat_area_start} sector")
        
        # Media Type
        f.seek(fat_area_start * 512)
        media_type = f.read(4)
        print("Media Type: " + ' '.join(f"{byte:02x}" for byte in media_type))
        
        #Partition status
        PST = f.read(4)
        print("Partition status: " + ' '.join(f"{byte:02x}" for byte in PST))
        
        # Data Area Calculation
        data_area_start = backup_fat_area_start + fat_size
        print(f"\n# Data Area")
        print(f"sector: {data_area_start}")
      
parsing("./etst.001")
