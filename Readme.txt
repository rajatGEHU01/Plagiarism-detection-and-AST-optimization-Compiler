> **DISCLAIMER:** This project is an educational research tool designed for code analysis and optimization. The plagiarism detection scores are based on AST (Abstract Syntax Tree) structural mapping and should be used as a supplementary reference, not as a definitive verdict on academic integrity.


--------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------
Markdown
## ⌨️ Execution Guide

To get the engine running locally, follow these precise steps:

### 1. Terminal 1: Launch Backend API
The backend handles the compilation, optimization, and plagiarism logic using FastAPI.
```bash
cd backend
# Install dependencies
pip install fastapi uvicorn 
# Start the server
uvicorn main:app --reload

--------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------
## 🌟 Overview
CodeLite++ Pro is a high-performance, hybrid development environment that combines a **Custom Compiler** with an **AI-Powered Code Analysis Engine**. Featuring a sleek, YouTube-inspired dark interface, it allows developers to write in a custom hybrid syntax, optimize it through AST transformations, and detect structural logic theft.

### 🛠️ Key Features
* **Hybrid Compiler:** Supports a unique blend of C++ declarations and Python control flow.
* **AST Optimizer:** Advanced "Constant Folding" and "Algebraic Identity" rules to simplify code.
* **Plagiarism Radar:** Uses structural fingerprinting (AST mapping) and token normalization to detect logic theft—even if variable names are changed.
* **Modern UI:** A futuristic YouTube/Amazon-themed dashboard with real-time result animations.

---

## 📜 The CodeLite++ Language Spec
CodeLite++ is designed to feel familiar to both C++ and Python developers.

### 1. Data Types & Variables
Variables are declared using C++ style types but support dynamic initialization.
```cpp
int x = 10
float pi = 3.14
string name = "Gemini"
2. Control Flow
Uses Python-style colons and indentation for blocks.

C++
if x > 5:
    print "High"
else:
    print "Low"

while x:
    print x
    x--
3. Functions
Functions use the func keyword and support return values.

C++
func add_tax(amount):
    int rate = 10
    return amount + rate
4. Custom Operators
++ : Increment (C++ Style)

-- : Decrement (C++ Style)

+, -, *, / : Standard Math

🧪 Testing Samples
Sample A: Optimization Test
Input:

C++
int base = 50 + 50
int multiplier = 1
int total = base * multiplier
print total
Optimized Result:
The engine will fold 50 + 50 to 100 and remove the * 1 identity math.

Sample B: Plagiarism Detection
If you compare these two, the engine will flag them as highly similar despite name changes:
Code 1: int a = 5
Code 2: int my_variable = 5



🏗️ Project Structure
/backend: FastAPI server and Compiler logic (tokenizer, parser, optimizer).

/frontend: YouTube-themed UI, app.js logic, and static/ assets.

/compiler: Core AST node definitions and plagiarism logic.
