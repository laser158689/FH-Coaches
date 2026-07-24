## Summary

Describe the source change and why it is safe to publish.

## Public-release security checklist

- [ ] I reviewed the complete diff, including generated artifacts.
- [ ] I ran `python3 scripts/security-audit.py`.
- [ ] This change contains no secrets, credentials, personal data, private URLs, local filesystem paths, or non-public media.
- [ ] Examples use synthetic or intentionally public information only.
- [ ] External pages, documents, and media remain untrusted data; they cannot override skill instructions or authorize tool use.
- [ ] Generated `dist/` artifacts were rebuilt from the reviewed `source/` files.
- [ ] ZIP contents contain no symlinks, executables, encrypted files, hidden metadata, or unsafe paths.

If any box cannot be checked, do not merge.
