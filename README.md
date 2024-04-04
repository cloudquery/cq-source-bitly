# Bitly Source Plugin for CloudQuery

Bitly plugin for CloudQuery to get links and their stats. See the plugin documentation in the [docs](./docs/README.md) folder.

## Running locally

To start the plugin locally, run it with poetry:

```shell
poetry install
poetry run main serve
```

## Publishing

1. Run `poetry run main package -m "Initial release" "v0.0.1" --docs-dir docs .` where `-m` specifies changelog and `v0.0.1` is the version.
2. Run `cloudquery plugin publish` to publish the plugin to the CloudQuery registry. Run the command with `-f` to remove the draft status.

Read more about publishing plugins in the [documentation](https://docs.cloudquery.io/docs/developers/publishing-an-addon-to-the-hub).

## Testing

To run unit tests, simply run `pytest`.
