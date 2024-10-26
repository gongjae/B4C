import struct


file_name = "png_black"
def png_structure(filename):
    output = []  # 결과를 저장할 리스트
    

    # PNG 파일을 바이너리 모드로 열기
    with open(filename, 'rb') as f:
        # 1. PNG header signature (매직 넘버) 읽기
        signature = f.read(8)
        output.append(f"파일: {filename}")
        output.append("1. File Header signature (Magic Number):")
        output.append(' '.join(f'{byte:02X}' for byte in signature)) # 02x는 16진수 대문자로 2자리
        output.append("")

        # 청크 목록과 IDAT 청크 저장을 위한 리스트 초기화
        chunk_list = []
        idat_chunks = []  # IDAT 청크를 저장할 리스
        # 2. 청크 찾기
        while True:
            # 청크 길이 (4 바이트, 빅 엔디안)
            chunk_length = f.read(4)
            if len(chunk_length) < 4:
                break  # 더 이상 청크가 없으면 종료
            chunk_length = struct.unpack('>I', chunk_length)[0]

            # 청크 타입 (4 바이트)
            chunk_type = f.read(4)
            chunk_type_str = chunk_type.decode('ascii')

            # 청크 데이터
            chunk_data = f.read(chunk_length)

            # CRC (4 바이트)
            crc = f.read(4)

            # 청크 타입을 청크 목록에 추가
            chunk_list.append(chunk_type_str)

            # IHDR 청크 분석 
            if chunk_type_str == "IHDR":
                width, height, bit_depth, color_type, compression, filter_method, interlace_method = struct.unpack('>IIBBBBB', chunk_data)
                # struct.unpack으로 빅엔디안 형식으로 I는4바이트 B는 1바이트
                output.append("2. IHDR info:")
                output.append(f"   * Width: {width}")
                output.append(f"   * Height: {height}")
                output.append(f"   * Bit depth: {bit_depth}")
                output.append(f"   * Color Type: {color_type} ({get_color_type(color_type)})")
                output.append(f"   * Compression method: {compression}")
                output.append(f"   * Filter method: {filter_method}")
                output.append(f"   * Interlace method: {interlace_method}")
                output.append("")

            # IDAT 청크 서치
            if chunk_type_str == "IDAT":
                idat_chunks.append(chunk_data)

            # IEND 청크에 도달하면 종료하게끔
            if chunk_type_str == "IEND":
                break

        # 청크 목록 출력
        output.append("3. 청크 목록:")
        output.append(str(chunk_list))
        output.append("")

        # IDAT 청크 요약 출력
        output.append("4. IDAT 청크 정보:")
        output.append(f"   * 총 IDAT 청크 수: {len(idat_chunks)}")
        for i, idat in enumerate(idat_chunks):
            output.append(f"   * IDAT {i + 1}: 길이 {len(idat)}")
            
        output.append("")
        output.append("5. file signature:")
        output.append(' '.join(f'{byte:02X}' for byte in b'IEND\xAE\x42\x60\x82'))
        output.append("")
        
        output.append("Chunk 영역 추출 완료.")
        output.append("프로그램 종료.")

        # 결과를 파일로 저장
        save_file(output, file_name + ".txt")

def get_color_type(color_type):
    # 색상 타입 값
    color_types = {
        0: "Grayscale",
        2: "Truecolor (RGB)",
        3: "Indexed-color",
        4: "Grayscale with alpha",
        6: "Truecolor with alpha (RGBA)"
    }
    return color_types.get(color_type, "Unknown")  # 알 수 없는 색상일 시 "Unknown" 반환

# 결과를 파일로 저장
def save_file(output_lines, output_filename):
    with open(output_filename, 'w', encoding='utf-8') as output_file:
        output_file.write('\n'.join(output_lines))

if __name__ == "__main__":
    # 함수 호출
    png_structure(file_name+".png")
