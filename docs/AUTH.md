# ATOS Gateway Authentication

## Boundary

Gateway authentication controls use of gateway transport and computing
resources. On-chain controller signatures control protocol state. A gateway
credential cannot replace, strengthen, or weaken contract authorization.

## Scopes

The Native service defines two minimum scopes:

| Scope | Permission |
|---|---|
| `native:read` | resolve finalized Agent and Capability state |
| `native:relay` | submit an already signed Native action for relay |

Gateways may define administrative scopes for their own operations, but those
scopes have no cross-gateway protocol meaning.

## Bearer transport

The reference gateway accepts an OAuth-style bearer token over TLS. Missing,
expired, revoked, or malformed tokens are unauthenticated. A valid token without
the required scope is denied. Tokens are never included in action hashes,
contract cells, chain transactions, logs, or portable evidence.

## Device authorization

A wallet or command-line client may use device authorization:

1. request a device code with explicit scopes;
2. show the verification URI and user code;
3. obtain user approval through a separate authenticated channel;
4. poll within the stated interval and expiry;
5. receive bounded access and refresh tokens; and
6. support refresh, revocation, and device removal.

The approval screen must distinguish permission to use a gateway from the
separate wallet confirmation of an on-chain action.

## Wallet signing

Before signature, wallets display at least network, object, action kind,
generation, sequence, predecessor, registry code identity, and payload-specific
effects. Capability transfer displays both owners. Quote acceptance displays
version, provider, endpoint, signer, maximum price, asset, expiry, escrow, and
dispute terms.

Private keys remain in the wallet or isolated signer. Recovery keys should be
kept separately from ordinary online action keys.

## Service accounts

Automated clients use narrowly scoped, short-lived credentials and separate
controller policies where on-chain signing is required. Gateway service
credentials must not be treated as controller keys.

## Security requirements

- TLS is mandatory outside loopback development.
- Token storage is encrypted and excluded from logs.
- Refresh tokens rotate and replay is detected.
- Device codes are high entropy, short-lived, single use, and rate limited.
- Scope elevation requires fresh approval.
- Authentication failure does not reveal whether an object or account exists.
- Public reads are bounded even if a gateway chooses to permit anonymous use.
