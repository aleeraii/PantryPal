module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    // Enforce scope to one of the known sub-projects or cross-cutting concerns
    'scope-enum': [
      2,
      'always',
      ['mobile', 'backend', 'frontend', 'ai', 'root', 'ci', 'deps'],
    ],
    // Warn (not error) when scope is omitted — encourages but doesn't block
    'scope-empty': [1, 'never'],
    // Disallow capitalised subject lines
    'subject-case': [
      2,
      'never',
      ['sentence-case', 'start-case', 'pascal-case', 'upper-case'],
    ],
    // Subject must not end with a period
    'subject-full-stop': [2, 'never', '.'],
    // Body must have a blank line before it
    'body-leading-blank': [2, 'always'],
    // Footer must have a blank line before it
    'footer-leading-blank': [2, 'always'],
    // Max header length
    'header-max-length': [2, 'always', 100],
  },
};
