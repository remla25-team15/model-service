# model-service

We recommend running the entire application to in development mode instead of trying to run this service by itself. 
Instructions can be found here: https://github.com/remla25-team15/operation?tab=readme-ov-file#development-section

## Instructions for creating a new release

To check the current version of the app run:

```zsh
bumpver show
```

We use `-alpha` to tag a pre-release instead of `-pre`.

Incrementing from alpha-release to stable is a conscious decision, so to make a stable release remove `-alpha`
from the version, e.g. is the current version is `1.0.14-alpha` you can run

```zsh
bumpver update --set-version "1.0.14" --dry  # Remove --dry to execute
```

After this is done, you can create a matching git tag by prefixing the version with `v`,
e.g.

```zsh
git tag v1.0.14
```

Then push the tag to origin and this will trigger a release workflow and update `main` to the next alpha release.

## Pre-Release workflow

This project supports creating pre-release versions tagged with a structured
format to help manage multiple experimental versions concurrently, especially
across feature branches.

### Tag format

Pre-release tags follow this pattern:

```
<base-version>-alpha.<branch-name>.<counter>
```

- **base-version**: The next alpha release of the latest stable version this branch is based on.  
  For example, if the latest stable release is `v2.0.2`, then this branch is based on `v2.0.3-alpha`.
- **branch-name**: The feature or experimental branch name (slashes replaced by dashes)
- **counter**: An auto-incrementing integer that counts pre-releases for this branch

**Example:**

```
2.0.3-alpha.feature-x.1
2.0.3-alpha.feature-x.2
2.0.3-alpha.bugfix-123.1
```

### Creating a pre-release tag

1. Ensure your working directory is clean (no uncommitted changes).
2. Pull the latest tags from origin:

   ```bash
   git fetch --tags
   ```

3. Run the tagging script `tag-pre-release.sh`, which:

   - Detects the current base version (using `bumpver`)
   - Determines the branch name and increments the counter for pre-release tags
   - Prompts for confirmation before creating and pushing the tag

4. After pushing the tag, the CI/CD workflow automatically builds and publishes
   the pre-release Docker images and creates a GitHub pre-release entry.

This workflow was designed to achieve the following:

- Supports multiple concurrent pre-releases from different branches without version conflicts
- Tags are predictable and easy to understand
- Prevents accidental overwriting of pre-release versions
- Enables team members to test experimental features independently

There might be a better way to do this, and we're open to feedback.

