import animator
import pathfinder

if __name__ == "__main__":
    with open("config.txt", "r") as config_file:
        data = config_file.readlines()
        
        if data[10].strip() == "yes":
            animator.main()
        else: 
            pathfinder.main(print_path = True)


