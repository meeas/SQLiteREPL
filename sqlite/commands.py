def meta_command(connection, user_input):
    """Swap sqlite3 meta commands with equivelant SQL queries"""
    user_parts = user_input.split()
    replaced = ''

    # .tables: print list of tables in database
    if user_parts[0].lower() == '.tables' or user_parts[0].lower() == '.table':
        replaced = 'SELECT name FROM sqlite_master WHERE type = "table";'

    # .schema: print details about a tables column
    elif user_parts[0].lower() == '.schema':
        if len(user_parts) == 1:
            replaced = 'SELECT sql FROM sqlite_master WHERE type = "table";'
        elif len(user_parts) == 2:
            s = 'SELECT sql FROM sqlite_master WHERE type = "table" AND name = "{[1]}";'
            replaced = s.format(user_parts)
        else:
            print('Usage: .schema [table]')

    # .dump: print SQL commands to recreate table
    # ToDo: http://www.sqlitetutorial.net/sqlite-dump/
    elif user_parts[0].lower() == '.dump':
        if len(user_parts) == 1:
            for line in connection.iterdump():
                print(line)
        elif len(user_parts) == 2:
            replaced = 'SELECT * from {[1]};'.format(user_parts)
        else:
            print('Usage: .dump [table]')

    else:
        print('That sqlite3 meta command has not been implimented')

    return replaced
