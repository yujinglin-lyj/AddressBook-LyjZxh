# AddressBook-LyjZxh

## Team Address Book

> A collaborative Software Engineering assignment implementing a feature-rich Contact Management System using Python Flask and Pandas.

## Course Information

| Item | Details                                         |
| :--- |:------------------------------------------------|
| **Course** | Software Engineering                            |
| **Team Name** | LyjZxh                                          |
| **Members** | Zhang Xiaohan, Lin Yujing |
---

##  Key Features

This project implements all required functionalities with a focus on user experience (UX) and data integrity.

### 1.  Smart Bookmarking (Requirement 1.1)
- Users can toggle the **"Favorite" (★)** status of any contact.
- Favorite contacts are highlighted with a golden star and prioritized in the UI.

### 2. Multi-Contact Tags (Requirement 1.2)
- **Dynamic Tagging System:** Unlike simple text fields, we implemented a dynamic tagging system.
- Users can add multiple contact methods (Mobile, Email, WeChat, etc.) with specific types.
- **Visual Distinction:** Different contact types are rendered with distinct colored badges (e.g., Mobile is Blue, Email is Green).

### 3.  Excel Integration (Requirement 1.3)
- **Export:** One-click export of all contact data to a formatted `.xlsx` file.
- **Smart Import:** - Supports importing external Excel files.
  - **Append Logic:** Newly imported data is appended to the existing list rather than overwriting it, ensuring no data loss.

### 4. Web Architecture
- Built with **Python Flask** (Backend) and **Bootstrap 5** (Frontend).
- Responsive design that works on desktop and mobile views.

---

##  Installation & Setup

Follow these steps to run the project locally.

### 1. Prerequisites
Ensure you have Python 3.8+ installed.

### 2. Install Dependencies
Run the following command to install Flask and data processing libraries:

```bash
pip install flask pandas openpyxl
