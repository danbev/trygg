package test_license

import future.keywords
import data.license.allow

licenses := [{"name": "MIT Licence"}, {"name": "Apache-License 2.0"}, {"name": "something"}]

test_allow if {
    r := allow with input as licenses
    r == true
}
