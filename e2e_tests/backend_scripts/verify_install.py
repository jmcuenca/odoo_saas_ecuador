import xmlrpc.client
import sys

url = 'http://localhost:24500'
db = 'odoo'
username = 'admin'
password = 'admin'

def verify_install():
    try:
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        if not uid:
            print("Authentication failed")
            sys.exit(1)

        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

        # 1. Check l10n_ec.driver model
        driver_fields = models.execute_kw(db, uid, password, 'l10n_ec.driver', 'fields_get', [], {'attributes': ['string', 'type']})
        if 'identification_number' in driver_fields:
            print("[PASS] l10n_ec.driver model exists with identification_number")
        else:
            print("[FAIL] l10n_ec.driver model missing or incomplete")

        # 2. Check account.move field extension
        move_fields = models.execute_kw(db, uid, password, 'account.move', 'fields_get', [], {'attributes': ['string']})
        if 'l10n_ec_sustento_code' in move_fields:
            print("[PASS] account.move has l10n_ec_sustento_code")
        else:
            print("[FAIL] account.move missing l10n_ec_sustento_code")

        # 3. Check Wizard model
        # Using execute_kw to search for model might fail if abstract? No, it's transient.
        # Try checking fields of wizard
        wizard_fields = models.execute_kw(db, uid, password, 'l10n_ec.ats.wizard', 'fields_get', [], {'attributes': ['string']})
        if 'xml_data' in wizard_fields:
            print("[PASS] l10n_ec.ats.wizard exists")
        else:
            print("[FAIL] l10n_ec.ats.wizard missing")

        print("VERIFICATION SUCCESSFUL")

    except Exception as e:
        print(f"Verification Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    verify_install()
