from faker import Faker
import sqlite3
import os
import random

# Initialize Faker
fake = Faker()

# Constants
OFFICE_LOCATIONS = [
    'Ashville, SC', 'Lucerne, CH', 'Austin, TX', 'Berlin, DE', 
    'Toronto, CA', 'Chicago, IL', 'Bloomington, IN'
]

REQUIRED_ROLES = {
    'Scrum Master': 1,
    'Product Owner': 1,
    'Tech Lead': 1,
    'Engineering Manager': 1,
    'Senior Developer': 2
}

def connect_db():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.abspath(os.path.join(script_dir, '../..'))
    db_path = os.path.join(base_dir, 'instance', 'flaskr.sqlite')
    print(db_path)
    return sqlite3.connect(db_path)

def create_contacts(db, num_products):
    """
    Create contacts for all products ensuring proper role coverage.
    Returns a dictionary mapping roles to lists of contact IDs.
    """
    cursor = db.cursor()
    contacts_by_role = {role: [] for role in REQUIRED_ROLES}
    
    # Calculate total needed contacts per role
    for role, per_product in REQUIRED_ROLES.items():
        total_needed = num_products * per_product
        print(f"Creating {total_needed} contacts for role: {role}")
        
        for _ in range(total_needed):
            first_name = fake.first_name()
            last_name = fake.last_name()
            
            cursor.execute('''
                INSERT INTO contacts (first_name, last_name, email, chat_username, location, role)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                first_name,
                last_name,
                f"{first_name.lower()}.{last_name.lower()}@sc1701d.com",
                f"@{first_name.lower()}{last_name.lower()}",
                random.choice(OFFICE_LOCATIONS),
                role
            ))
            contacts_by_role[role].append(cursor.lastrowid)
    
    return contacts_by_role

def create_product(db, product_num, contacts_by_role):
    """Create a single product with all required role assignments."""
    cursor = db.cursor()
    
    # Create product
    product_name = fake.catch_phrase()
    cursor.execute('''
        INSERT INTO products (name, body)
        VALUES (?, ?)
    ''', (product_name, fake.paragraph()))
    product_id = cursor.lastrowid
    
    # Create repository
    repo_name = f"{product_name.lower().replace(' ', '-')}-repo"
    cursor.execute('''
        INSERT INTO repositories (product_id, name, url)
        VALUES (?, ?, ?)
    ''', (
        product_id,
        repo_name,
        f"https://github.com/sc1701d/{repo_name}"
    ))
    
    # Assign contacts for each role
    for role, count in REQUIRED_ROLES.items():
        available_contacts = contacts_by_role[role]
        selected_contacts = random.sample(available_contacts, count)
        
        for contact_id in selected_contacts:
            cursor.execute('''
                INSERT INTO product_contacts (product_id, contact_id)
                VALUES (?, ?)
            ''', (product_id, contact_id))

def main():
    NUM_PRODUCTS = 500
    print(f"Starting database population with {NUM_PRODUCTS} products...")
    
    conn = connect_db()
    try:
        print("Creating contacts...")
        contacts_by_role = create_contacts(conn, NUM_PRODUCTS)
        
        print("Creating products and assigning contacts...")
        for i in range(NUM_PRODUCTS):
            if (i + 1) % 50 == 0:
                print(f"Created {i + 1} products...")
            create_product(conn, i + 1, contacts_by_role)
            
        conn.commit()
        print("\nDatabase populated successfully!")
        
        # Print summary
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM products")
        product_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM contacts")
        contact_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM product_contacts")
        assignment_count = cursor.fetchone()[0]
        
        print(f"\nSummary:")
        print(f"Products created: {product_count}")
        print(f"Contacts created: {contact_count}")
        print(f"Role assignments created: {assignment_count}")
        
    except Exception as e:
        print(f"Error occurred: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    main()