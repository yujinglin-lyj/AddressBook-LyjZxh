# Address Book-LyjZxh

> A collaborative Software Engineering assignment implementing a feature-rich Contact Management System using Python Flask and Pandas.

## Course Information

| Item | Details |
| --- | :--- |
| **Course** | Software Engineering |
| **Team Name** | LyjZxh |
| **Members** | Zhang Xiaohan, Lin Yujing |

---

## Key Features

This project implements all required functionalities with a focus on User Experience (UX) and Data Integrity.

### 1. Smart Bookmarking and Filtering (Requirement 1.1)
- **Toggle Favorites:** Users can toggle the "Favorite" status of any contact.
- **Visual Priority:** Favorite contacts are highlighted with a star icon.
- **One-Click Filter:** Implemented a "Show Favorites Only" filter mode, allowing users to quickly isolate and view important contacts without scrolling through the entire list.

### 2. Dynamic Multi-Contact Tagging (Requirement 1.2)
- **Interactive Badge System:** Unlike simple text fields, we implemented a dynamic tagging system.
- **Multi-Type Support:** Users can associate multiple contact details (Mobile, Email, WeChat, Work, etc.) with a single contact.
- **Visual Distinction:** Different contact types are rendered with distinct colored badges (e.g., Mobile is Blue, Email is Green) for immediate recognition.
- **Input Validation:** Prevents accidental form submission when pressing "Enter", improving data entry stability.

### 3. Advanced Excel Integration (Requirement 1.3)
- **Export:** One-click export of all contact data to a formatted `.xlsx` file.
- **Non-Destructive Import:** Supports importing external Excel files. We implemented specific "Append Logic" using Pandas (pd.concat), ensuring that newly imported data is merged with the existing list rather than overwriting it.

### 4. Web Architecture (Requirement 1.4)
- **Backend:** Built with Python Flask for lightweight and efficient data processing.
- **Frontend:** Designed with Bootstrap 5 to ensure a responsive layout that works on both desktop and mobile views.
- **Deployment:** Compatible with WSGI servers (e.g., PythonAnywhere) for cloud deployment.

---

## Installation & Setup

Follow these steps to run the project locally.

### 1. Prerequisites
Ensure you have Python 3.8 or higher installed on your system.

### 2. Install Dependencies
Open your terminal or command prompt in the project directory and run the following command to install Flask and data processing libraries:

```bash
pip install flask pandas openpyxl
