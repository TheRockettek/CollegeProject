import { test, expect } from '@playwright/test';

const WEBSITE_URL = process.env.WEBSITE_URL || 'http://localhost:5000';

test('visit the app root url', async ({ page }) => {
  await page.goto(WEBSITE_URL);

  // Check the page header. We should be logged out.
  await expect(page.locator('form h1')).toHaveText('Welcome to')
  await expect(page.locator('form h2')).toHaveText('WebbiSkools QuizManager')
});

test('failed login shows popup', async ({ page }) => {
  await page.goto(WEBSITE_URL);

  // Check the page header. We should be logged out.
  await expect(page.locator('form h1')).toHaveText('Welcome to')
  await expect(page.locator('form h2')).toHaveText('WebbiSkools QuizManager')

  // Login with wrong password
  await page.fill('input[id="username"]', 'admin');
  await page.fill('input[id="password"]', 'wrongpassword');
  await page.click('[type="submit"]');

  // Check for the toast message.
  await expect(page.locator('#toast-default')).toContainText('Invalid username or password');
});

// Setup the users we want to test.

const users = [
  {
    name: 'Admin',
    username: 'admin',
    password: 'password',
    role: 'editor',
    canSeeAnswers: true,
    canEditanswers: true,
  },
  {
    name: 'Teacher',
    username: 'teacher',
    password: 'password',
    role: 'viewer',
    canSeeAnswers: true,
    canEditanswers: false,
  },
  {
    name: 'Student',
    username: 'student',
    password: 'password',
    role: 'restricted',
    canSeeAnswers: false,
    canEditanswers: false,
  }
];

users.forEach((user) => {

  test(`successful login as ${user.username}`, async ({ page }) => {
    await page.goto(WEBSITE_URL);

    // Login as the user.
    await page.fill('input[id="username"]', user.username);
    await page.fill('input[id="password"]', user.password);
    await page.click('[type="submit"]');

    // Check the page header for our name and role.
    await expect(page.locator('nav').filter({ hasText: user.name })).toContainText(user.name);
    await expect(page.locator('nav').filter({ hasText: user.role })).toContainText(user.role);
  });

  test(`view quiz as ${user.username} (${user.role})`, async ({ page }) => {
    await page.goto(WEBSITE_URL);

    // Login as the user.
    await page.fill('input[id="username"]', user.username);
    await page.fill('input[id="password"]', user.password);
    await page.click('[type="submit"]');

    // Check the page header.
    await expect(page.locator('h1')).toHaveText('All Quizzes');

    // Get the text of the first column in the table.
    const firstColumnText = await page.locator('table tbody tr').first().locator('td').first().textContent();

    // Click on the first Edit/View link in the table.
    await page.click('table tr a');

    // Validate the header at the top of the page we navigated to is equal to the quiz name in the table.
    await expect(page.locator('h1')).toHaveText(firstColumnText);

    if (user.canEditanswers) {
      // If we can edit answers, make sure the Edit Answers button is showing.
      await expect(page.locator('button').filter({ hasText: 'Edit Answers' }).first()).toHaveText('Edit Answers');
    } else if (user.canSeeAnswers) {
      // If we can only see answers, make sure the Show Answers button is showing.
      await expect(page.locator('button').filter({ hasText: 'Show Answers' }).first()).toHaveText('Show Answers');
    } else {
      // If we cannot edit or show answers, make sure both buttons are not present on the page.
      await expect(page.locator('button').filter({ hasText: 'Edit Answers' })).toHaveCount(0);
      await expect(page.locator('button').filter({ hasText: 'Show Answers' })).toHaveCount(0);
    }
  });
});
