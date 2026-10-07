def hanoi_iterative_simple(n, source, target, auxiliary):
    total_moves = (1 << n) - 1  # 2^n - 1
    
    if n % 2 == 0:
        pegs = [source, auxiliary, target]
    else:
        pegs = [source, target, auxiliary]

    # Track disk positions
    disk_pos = [0] * (n + 1)

    for i in range(1, total_moves + 1):
        # Disk number to move matches the 1-based index of the lowest set bit
        disk = (i & -i).bit_length()

        from_idx = disk_pos[disk]
        
        # Disk 1 always moves +1 cyclic step (0 -> 1 -> 2 -> 0)
        # Disk d moves in direction determined by disk parity relative to cyclic order
        if disk % 2 == 1:
            to_idx = (from_idx + 1) % 3
        else:
            to_idx = (from_idx + 2) % 3  # Equivalent to -1 mod 3

        disk_pos[disk] = to_idx

        print(f"Move disk {disk} from {pegs[from_idx]} to {pegs[to_idx]}")


def main():
    number_plates = 3
    first_pole = 'A'
    target_pole = 'C'
    helping_pole = 'B'
    
    print(f"=== Tower of Hanoi with ({number_plates} plates) ===")
    print(f"Move the disc from Pole {first_pole} to Pole {target_pole} using Pole {helping_pole}\n")
    
    # Corrected function call name
    hanoi_iterative_simple(number_plates, first_pole, target_pole, helping_pole)

    total = 2**number_plates - 1
    print(f"\nFinish on {total} step iteration!")
    
if __name__ == "__main__":
    main()