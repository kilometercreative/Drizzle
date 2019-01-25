# Drizzle Deploy

**local.sh** builds drz and installs it.

**test.sh** uploads to test.pypi.org

**upload.sh** uploads to pypi.org

---

#### Instructions for initializing drizzle:
1. Go into your AWS account and navigate to the **IAM** page.
2. Go to the **Users** tab on the right-hand side
3. Click **Add User** in the top-left hand corner
4. Pick any username (although "drizzle" makes sense) and check
 the box for **Programmatic Access** but not AWS Management
Console access. Click "Next: Permissions" in the bottom right.
5. Under "Set permissions", click **Attach existing policies 
directly**. Then search for and select the "AdministratorAccess" 
policy. Click "Next: Review" in the bottom right.
6. Click **Create User**
7. Download these credentials and use them to set up Drizzle.