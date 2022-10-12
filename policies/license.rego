package license

import future.keywords

default allow = "false"

allow if {
  some l in input
    l.name = "Apache-License 2.0"
}
