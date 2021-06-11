from io import BufferedReader
import random
from typing import List
import heapq
import concurrent.futures

def generate_ints(file_path, n_ints):
    with open(file_path, 'wb') as file:
        print(f'Generating {n_ints} random ints...')
        for _ in range(n_ints):
            file.write(random.getrandbits(32).to_bytes(4, 'big'))
    print(f'Generated {n_ints} random ints from 0 to {n_ints}')

def external_sort(input_file: str, output_file: str, chunk_size: int) -> str:
    
    def sort_in_chunks(input_file: str, chunk_size: int) -> List[str]:
        buffer: List[int] = []
        files = []

        chunk_id = 0

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures: List[concurrent.futures.Future] = []

            with open(input_file, 'rb') as file:
                while True:
                    bytes = file.read(4)
                    if len(bytes) == 0: 
                        if len(buffer) > 0: 
                            futures.append(executor.submit(sort_chunk, buffer, chunk_id))
                        break
                    buffer.append(int.from_bytes(bytes, 'big'))
                    if len(buffer) == chunk_size:
                        futures.append(executor.submit(sort_chunk, buffer, chunk_id))
                        chunk_id += 1
                        buffer = []
        
            for future in concurrent.futures.as_completed(futures):
                files.append(future.result())    

        print(f'Generated {len(files)} intermediate files')

        return files

    def sort_chunk(chunk: List[int], chunk_id: int) -> str:
        # in-memory sort
        chunk.sort()
        # write to intermediate file
        file_name = f'intermediate_{chunk_id}.bin'
        with open(file_name, 'ab') as intermediate_file:
            for x in chunk: 
                intermediate_file.write(x.to_bytes(4, 'big'))
        print(f'Wrote {len(chunk)} sorted ints to {file_name}')
        return file_name 

    def read_int(file: BufferedReader) -> int:
        bytes = file.read(4)
        if len(bytes) == 0: return None
        return int.from_bytes(bytes, 'big')

    def merge(intermediate_files: List[str], output_file: str) -> str:
        file_handles: List[BufferedReader] = [open(file_name, 'rb') for file_name in intermediate_files]
        
        heap = []
        for i, file_handle in enumerate(file_handles):
            heapq.heappush(heap, (read_int(file_handle), i))

        print('Merging in progress...')
        with open(output_file, 'wb') as output:
            while heap:
                number, file_handle_index = heapq.heappop(heap)
                output.write(number.to_bytes(4, 'big'))
                next_number = read_int(file_handles[file_handle_index])
                if next_number is not None:
                    heapq.heappush(heap, (next_number, file_handle_index))
        
        for file_handle in file_handles:
            file_handle.close()
        
        return output_file

    intermediate_files = sort_in_chunks(input_file, chunk_size)
    return merge(intermediate_files, output_file)

def main():
    INPUT_FILE, OUTPUT_FILE = 'unsorted.bin', 'sorted.bin'
    N_INTS = 1_000_000_000
    SIZE_PER_INTERMEDIATE_FILE = 10_000_000

    #generate_ints(INPUT_FILE, N_INTS)
    print('Sorting complete:', external_sort(INPUT_FILE, OUTPUT_FILE, SIZE_PER_INTERMEDIATE_FILE))

if __name__ == "__main__":
    main()