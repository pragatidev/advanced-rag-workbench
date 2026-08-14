# ACME access control policy (AC-2)

Account management follows the AC-2 control family. Human accounts are provisioned by identity ops. Service accounts are provisioned by platform ops. Every account has an owner, a review date, and a tenant tag.

Tenant helix-east may read helix-east documents only. Tenant helix-west may read helix-west documents only. Shared runbooks are tagged tenant=shared.

Disable accounts within 24 hours of a role change. Shared passwords are forbidden. Privileged actions write an audit row.
