# 🚀 Complete Setup Guide - Cannacraft Selenium Tests

## ❌ Why Tests Failed

Your tests failed because:
1. **Missing HTML file in repository** - The test looks for `index.html` but it wasn't found
2. **File path issues** - GitHub Actions couldn't locate the HTML file
3. **ChromeDriver compatibility** - Older ChromeDriver download method

## ✅ Solution - Step by Step Setup

### Step 1: Create Proper Repository Structure

```
your-repository/
├── index.html                    # Your website (REQUIRED!)
├── test_cannacraft.py           # Test suite
├── requirements.txt             # Dependencies
├── pytest.ini                   # Pytest config
├── .github/
│   └── workflows/
│       └── selenium-tests.yml   # CI/CD workflow
├── .gitignore                   # Git ignore file
└── README.md                    # Documentation
```

### Step 2: Create/Save All Required Files

#### 2.1 Save the HTML File
Create `index.html` in your repository root with the HTML content from the document.

#### 2.2 Create `.gitignore`
```bash
# Create .gitignore file
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Testing
.pytest_cache/
.coverage
htmlcov/
*.html
coverage.xml
report.html

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
EOF
```

#### 2.3 Create `requirements.txt`
```txt
selenium==4.15.2
pytest==7.4.3
pytest-html==4.1.1
pytest-cov==4.1.0
webdriver-manager==4.0.1
```

#### 2.4 Create `pytest.ini` (optional but recommended)
Use the pytest.ini content provided above.

### Step 3: Initialize Git Repository (if not done)

```bash
# Initialize git repository
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Add Cannacraft website and test suite"

# Add remote (replace with your repository URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push to GitHub
git push -u origin main
```

### Step 4: Verify Local Setup

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify HTML file exists
ls -la index.html

# Run tests locally
pytest test_cannacraft.py -v
```

### Step 5: Setup GitHub Actions

#### 5.1 Create Workflow Directory
```bash
mkdir -p .github/workflows
```

#### 5.2 Create Workflow File
Save the updated GitHub Actions workflow to `.github/workflows/selenium-tests.yml`

#### 5.3 Verify Files Are Committed
```bash
# Check status
git status

# You should see:
# - index.html
# - test_cannacraft.py
# - requirements.txt
# - .github/workflows/selenium-tests.yml

# Add and commit
git add .
git commit -m "Add Selenium test suite with GitHub Actions"
git push origin main
```

### Step 6: Enable GitHub Actions

1. Go to your GitHub repository
2. Click on **Actions** tab
3. You should see the workflow running automatically
4. If not, click **"I understand my workflows, go ahead and enable them"**

### Step 7: Monitor Test Execution

1. Go to **Actions** tab in your repository
2. Click on the latest workflow run
3. Watch the real-time logs
4. Tests should now pass! ✅

## 🔍 Troubleshooting Common Issues

### Issue 1: "index.html not found"
**Solution:**
```bash
# Verify file exists in root
ls -la index.html

# If not, create it with your HTML content
# Then commit and push
git add index.html
git commit -m "Add index.html"
git push
```

### Issue 2: "ChromeDriver version mismatch"
**Solution:** The updated workflow automatically handles this. Just push the new workflow file.

### Issue 3: Tests timeout
**Solution:** Increase wait times in `test_cannacraft.py`:
```python
driver.implicitly_wait(20)  # Increase from 10 to 20
```

### Issue 4: "Module not found"
**Solution:** Ensure `requirements.txt` is in repository:
```bash
git add requirements.txt
git commit -m "Add requirements.txt"
git push
```

### Issue 5: GitHub Actions still fails
**Solution:** Check these:
1. All files are committed and pushed
2. index.html is in the repository root
3. Workflow file is in `.github/workflows/`
4. GitHub Actions is enabled in repository settings

## 📊 Expected Test Results

When everything is set up correctly, you should see:

```
test_cannacraft.py::TestCannacraftWebsite::test_page_load PASSED [ 5%]
test_cannacraft.py::TestCannacraftWebsite::test_navigation_buttons_present PASSED [ 10%]
test_cannacraft.py::TestCannacraftWebsite::test_home_page_content PASSED [ 15%]
test_cannacraft.py::TestCannacraftWebsite::test_navigate_to_address_page PASSED [ 21%]
test_cannacraft.py::TestCannacraftWebsite::test_address_form_fields_present PASSED [ 26%]
test_cannacraft.py::TestCannacraftWebsite::test_address_form_submission PASSED [ 31%]
test_cannacraft.py::TestCannacraftWebsite::test_address_form_validation PASSED [ 36%]
test_cannacraft.py::TestCannacraftWebsite::test_navigate_to_appointment_page PASSED [ 42%]
test_cannacraft.py::TestCannacraftWebsite::test_appointment_form_fields_present PASSED [ 47%]
test_cannacraft.py::TestCannacraftWebsite::test_appointment_form_submission PASSED [ 52%]
test_cannacraft.py::TestCannacraftWebsite::test_navigate_to_feedback_page PASSED [ 57%]
test_cannacraft.py::TestCannacraftWebsite::test_feedback_form_fields_present PASSED [ 63%]
test_cannacraft.py::TestCannacraftWebsite::test_star_rating_system PASSED [ 68%]
test_cannacraft.py::TestCannacraftWebsite::test_feedback_form_submission PASSED [ 73%]
test_cannacraft.py::TestCannacraftWebsite::test_feedback_form_validation PASSED [ 78%]
test_cannacraft.py::TestCannacraftWebsite::test_form_cancel_button PASSED [ 84%]
test_cannacraft.py::TestCannacraftWebsite::test_hero_button_navigation PASSED [ 89%]
test_cannacraft.py::TestCannacraftWebsite::test_responsive_elements PASSED [ 94%]
test_cannacraft.py::TestCannacraftWebsite::test_all_pages_accessibility PASSED [100%]

======================== 19 passed in 45.23s ========================
```

## 🎯 Quick Commands Cheat Sheet

```bash
# Local testing
pytest test_cannacraft.py -v

# Generate HTML report
pytest test_cannacraft.py -v --html=report.html --self-contained-html

# Run specific test
pytest test_cannacraft.py::TestCannacraftWebsite::test_page_load -v

# Run with coverage
pytest test_cannacraft.py --cov=. --cov-report=html

# Debug mode (see browser)
# Edit test file and comment out: chrome_options.add_argument("--headless")
pytest test_cannacraft.py -v -s

# Check what files git will commit
git status

# Push changes to GitHub
git add .
git commit -m "Your message"
git push origin main
```

## 📁 Final File Checklist

Before pushing to GitHub, ensure these files exist:

- [ ] ✅ `index.html` (in repository root)
- [ ] ✅ `test_cannacraft.py` (in repository root)
- [ ] ✅ `requirements.txt` (in repository root)
- [ ] ✅ `.github/workflows/selenium-tests.yml`
- [ ] ✅ `.gitignore` (optional but recommended)
- [ ] ✅ `pytest.ini` (optional)
- [ ] ✅ `README.md` (documentation)

## 🎉 Success Indicators

You'll know everything works when:

1. ✅ Local tests pass: `pytest test_cannacraft.py -v`
2. ✅ GitHub Actions shows green checkmark
3. ✅ Test report is available in Artifacts
4. ✅ All 19 tests pass

## 🆘 Still Having Issues?

If tests still fail:

1. **Check GitHub Actions logs:**
   - Go to Actions tab
   - Click on failed run
   - Read the error messages

2. **Verify file structure:**
   ```bash
   ls -la
   # Should show index.html in current directory
   ```

3. **Test locally first:**
   ```bash
   pytest test_cannacraft.py -v -s
   # -s flag shows print statements
   ```

4. **Check file contents:**
   ```bash
   # Verify HTML file has content
   head -20 index.html
   ```

## 📞 Need More Help?

Create a GitHub issue with:
- Error message from GitHub Actions
- Output of `git status`
- Output of `ls -la`
- Screenshot of Actions tab

---

**Good luck! You've got this! 🚀**