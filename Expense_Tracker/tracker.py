import pymysql

#connect to Mysql
connection = pymysql.connect(host='localhost',
                             user='bharath',
                             password='12345678',
                             db='expense_tracker',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


cursor = connection.cursor()


def get_category_id(name):
    cursor.execute('select id from categories where name = %s',(name))
    result = cursor.fetchone()
    if result:
        print(result['id'])
        return result['id']
    else:
        return None


def add_expense():
    amount = float(input('Enter the amount : '))
    description = input('Enter the description : ')
    date = input('Enter date in (YYYY-MM-DD) : ')
    category = input('Enter Category : ')

    cat_id = get_category_id(category)
    if not cat_id:
        print('Category not found in our database')
        print('First add the category to the database')
        return None
    cursor.execute('Insert into expenses(amount,description,date,category_id) values (%s , %s, %s, %s)',(amount,description,date,cat_id))
    connection.commit()
    print('Expense added successfully')

def view_expenses():
    cursor.execute('''select e.Id,e.amount, e.description, e.date, c.name as category
                        from expenses e
                        inner join categories c on e.category_id = c.Id''')
    result = cursor.fetchall()
    print("ID | Amount | Description | Date | category")
    for exp in result:
        print(str(exp['Id']) + "|" + str(exp['amount']) + "|" + str(exp['description']) + '|' + str(exp['date']) + "|" + str(exp['category']))
    
def add_category():
    try:
        name = input('Enter the new category name : ')
        cursor.execute('Insert into categories (name) values (%s)',(name))
        connection.commit()
        print('Category added')
    except Exception as e:
        print('Category already added')

def delete_expense():
    category = input('Enter category to delete (will delete all entries of that category)')
    cat_id = get_category_id(category)
    if not cat_id:
        print('category is not found in our database')
        return None
    
    cursor.execute("Delete from expenses where category_id = %s",(cat_id))
    connection.commit()
    print('Expense deleted successfully')

def total_by_month():
    month = input("Enter month (YYYY-MM): ")
    query = "SELECT SUM(amount) as total_sum,count(*) as total_count FROM expenses WHERE DATE_FORMAT(date, '%Y-%m') = '{}'".format(month)
    cursor.execute(query)
    total = cursor.fetchone()
    print(f"Total spent in {month}: ₹{total['total_sum'] if total else 0}")
    print(f"Total count in {month}: {total['total_count'] if total else 0}")

def total_by_category():
    category = input('Enter Category : ')
    cat_id = get_category_id(category)
    if not cat_id:
        print('Category not found in our database')
        return None
    
    query = "SELECT SUM(amount) as total_sum,count(*) as total_count FROM expenses WHERE category_id = {}".format(cat_id)
    cursor.execute(query)
    total = cursor.fetchone()
    print(f"Total spent in {category}: ₹{total['total_sum'] if total else 0}")
    print(f"Total count in {category}: {total['total_count'] if total else 0}")
