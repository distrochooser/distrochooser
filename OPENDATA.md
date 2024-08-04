# Open data access for distrochooser.de

## Decision tree

This versions decision matrix part of the repository in the subfolder `/doc/matrix`.

## Live data

Statistical data is published automatically from the `/data/<version>` endpoint. The endpoint data structure is defined by the `OpenDataV<version>` classes, defined in `code/kuusi/web/opendata.py`.

To use a specific version, see the table below.

|Definition|Endpoint|
|---|---|
|`OpenDataV1`|`/data/1`

Results are cached for the interval returned in `RefreshInterval`/ `NextUpdate`.

## Fair use

Please refrain from do heavy request counts on the open data endpoints. Keep you requests close to the `RefreshInterval` returned in the data.

## License

The dataset is made available under the Open Database License: http://opendatacommons.org/licenses/odbl/1.0/. Any rights in individual contents of the dataset are licensed under the Database Contents License: http://opendatacommons.org/licenses/dbcl/1.0/