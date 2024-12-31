from debate import Debate


def main():
    debate = Debate()
    thesis = str(input("Enter a thesis: "))
    debate.perform(thesis, rounds=2)

    
if __name__ == '__main__':
    main()
