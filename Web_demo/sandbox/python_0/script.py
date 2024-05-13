# To install the Hugging Face library, run:
# !pip install datasets

from datasets import load_dataset

def get_first_test_data_entry():
    # Load the dataset from Hugging Face
    dataset = load_dataset('nathanlauga/evalplus')

    # Get the test dataset
    test_dataset = dataset['test']

    # Get the first entry in the test dataset
    first_entry = test_dataset[0]

    return first_entry

# Call the function and print the first entry
first_entry = get_first_test_data_entry()
print("First entry:", first_entry)