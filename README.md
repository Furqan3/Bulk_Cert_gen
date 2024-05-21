# Certificate Generator

This Python script generates certificates for members based on data provided in a CSV file. It utilizes ReportLab for PDF generation and PyPDF2 for PDF manipulation.

## Requirements

- Python 3.x
- pandas
- reportlab
- PyPDF2
- Pillow (PIL)
- Ensure the necessary fonts and image files are available in the specified paths.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Furqan3/Bulk_Cert_gen.git
    ```

2. Navigate to the project directory:

    ```bash
    cd Bulk_Cert_gen
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Place your CSV file containing member data in the project directory.

2. Modify the script according to your file paths and column names as necessary.

3. Run the script:

    ```bash
    python certificate_generator.py
    ```

4. Certificates will be generated in the `certificates` directory.

## Configuration

- **CSV File**: Ensure your CSV file contains columns for member names and categories. Modify the script to match your column names.

- **Certificate Template**: Replace the placeholder certificate template (`Certificate.png`) with your own design. Make sure the template is in PNG format.

- **Font**: Specify the path to the font file (`Montserrat-SemiBold.ttf`). This font will be used for the certificate text.

## Customization

- **Text Positioning**: Adjust the text positioning and styling according to your certificate template. You can modify the font size, color, and alignment in the script.

- **Output Path**: Customize the output path for generated certificates as per your requirements.

## Error Handling

- The script includes error handling for missing files, missing columns in the CSV, and other potential exceptions during certificate generation. Error messages are logged for traceability.

## Contributing

Contributions are welcome! If you have any suggestions, improvements, or bug fixes, feel free to open an issue or create a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
