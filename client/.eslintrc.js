module.exports = {
    root: true,
    parser: '@typescript-eslint/parser',
    plugins: [
        '@typescript-eslint',
    ],
    extends: [
        'eslint:recommended',
        "plugin:react/recommended"
    ],
    "env": {
        "browser": true,
        "amd": true,
        "node": true
    },
};