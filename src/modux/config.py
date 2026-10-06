import getpass

import keyring


SERVICE_NAME = "Modux"
USERNAME = "groq-api-key"


def get_api_key():
    """
    Get the Groq API key.

    Priority:
    1. GROQ_API_KEY environment variable
    2. Operating system credential store
    """

    import os

    environment_key = os.getenv("GROQ_API_KEY")

    if environment_key:
        return environment_key.strip()

    try:
        stored_key = keyring.get_password(
            SERVICE_NAME,
            USERNAME,
        )

        if stored_key:
            return stored_key.strip()

    except Exception:
        pass

    return None


def save_api_key(api_key):
    """
    Save the API key using the operating system's
    secure credential storage.
    """

    if not api_key:
        return False

    try:
        keyring.set_password(
            SERVICE_NAME,
            USERNAME,
            api_key.strip(),
        )

        return True

    except Exception:
        return False


def delete_api_key():
    """
    Remove the stored API key.
    """

    try:
        keyring.delete_password(
            SERVICE_NAME,
            USERNAME,
        )

        return True

    except keyring.errors.PasswordDeleteError:
        return True

    except Exception:
        return False


def setup_api_key():
    print()
    print("================================")
    print("          MODUX SETUP")
    print("================================")
    print()
    print("Modux requires a Groq API key.")
    print()
    print("1. Open:")
    print("   https://console.groq.com/keys")
    print()
    print("2. Create a Groq API key.")
    print()
    print("3. Paste the key below.")
    print()
    print("Your key will NOT be displayed while typing.")
    print()

    api_key = getpass.getpass(
        "Groq API Key: "
    ).strip()

    if not api_key:
        print("\nNo API key entered.")
        return False

    if save_api_key(api_key):

        print()
        print("API key saved successfully.")
        print("It is stored using your operating system's")
        print("credential storage.")
        print()

        return True

    print()
    print("Could not securely save the API key.")
    print()
    print("You can still use the GROQ_API_KEY environment")
    print("variable as an alternative.")
    print()

    return False