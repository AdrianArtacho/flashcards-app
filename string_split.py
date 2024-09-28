def main(raw_string, verbose=False):

    if verbose:
        print("The given string is")
        print(raw_string)

        print("The strings after the split are")
    
    result = raw_string.split()
    
    if verbose:
        print(result)
    
    return result

if __name__ == "__main__":
    raw_string = "Hello Everyone Welcome"
    main(raw_string)