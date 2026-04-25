def log_section(title, data=""):
    """
    Print a formatted block of text for logging information in the terminal.
    It creates a clear visual section for each completed task using separators.
    The title is shown in uppercase and the content is displayed below the title.
    This can be printed either as [key: value pairs] (if it is a dictionary) or as plain text (any other data type).
    """

    # Section separator (top border)
    print("\n" + "=" * 60)
    # Print section title in uppercase for visibility
    print(title.upper())
    # Section separator (bottom border of header)
    print("=" * 60)

    # If data is a dictionary, print each key-value pair
    if isinstance(data, dict):
        for key, value in data.items():
            print(f"{key}: {value}")
    # Otherwise print raw data directly
    else:
        print(data)
