import argparse
import database


def main():
    """
    Main function to parse command-line arguments and manage links.
    """
    parser = argparse.ArgumentParser(description="Manage astrago shortlinks.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Add command
    parser_add = subparsers.add_parser("add", help="Add a new link.")
    parser_add.add_argument("name", help="The short name for the link.")
    parser_add.add_argument("url", help="The destination URL.")

    # Delete command
    parser_delete = subparsers.add_parser("delete", help="Delete a link.")
    parser_delete.add_argument("name", help="The name of the link to delete.")

    # Rename command
    parser_rename = subparsers.add_parser("rename", help="Rename a link.")
    parser_rename.add_argument("old_name", help="The current name of the link.")
    parser_rename.add_argument("new_name", help="The new name for the link.")

    args = parser.parse_args()

    # Ensure the table exists before doing anything
    database.create_table()

    if args.command == "add":
        url = args.url
        if not url.startswith("http://") and not url.startswith("https://"):
            url = f"https://{url}"
        if database.add_link(args.name, url):
            print(f"Successfully added link: {args.name} -> {url}")
        else:
            print(f"Error: Link '{args.name}' already exists.")
    elif args.command == "delete":
        if database.delete_link(args.name):
            print(f"Successfully deleted link: {args.name}")
        else:
            print(f"Error: Link '{args.name}' not found.")
    elif args.command == "rename":
        if database.rename_link(args.old_name, args.new_name):
            print(f"Successfully renamed link: {args.old_name} -> {args.new_name}")
        else:
            print(f"Error: Could not rename '{args.old_name}'. It may not exist or '{args.new_name}' may already be taken.")


if __name__ == "__main__":
    main()
