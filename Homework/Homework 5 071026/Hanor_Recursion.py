def hanoi_recursive(n, source, target, auxiliary):
    if n == 1:
        print(f"Move disk 1 from {source} to {target}")
        return
    
    hanoi_recursive(n - 1, source, auxiliary, target)
    
    print(f"Move disk {n} from {source} to {target}")
    
    hanoi_recursive(n - 1, auxiliary, target, source)

def main():
    number_plates = 3
    first_pole = 'A'
    target_pole = 'C'
    helping_pole = 'B'

    print(f"=== Tower of Hanoi with ({number_plates} plates) ===")
    print(f"Move the disc from Pole {first_pole} to Pole {target_pole} using Pole {helping_pole}\n")

    hanoi_recursive(number_plates, first_pole, target_pole, helping_pole)

    total = 2**number_plates - 1
    print(f"\nFinish on {total} step recursion!")


if __name__ == "__main__":
    main()
