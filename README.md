
# CityCatalyst
Open Source carbon accounting for cities

## Test coverage
[![codecov](https://codecov.io/github/Open-Earth-Foundation/CityCatalyst/graph/badge.svg?token=FD69J1XR6M)](https://app.codecov.io/github/Open-Earth-Foundation/CityCatalyst/tree/develop)

## Docs
### [CityCatalyst Readme](https://github.com/Open-Earth-Foundation/CityCatalyst/tree/develop/app#citycatalyst)

### [CityCatalyst API documentation & wiki](https://github.com/Open-Earth-Foundation/CityCatalyst/wiki)


## Local Development: Set up steps

#### Database

You have to create a Postgres database user:

```bash
createuser ccglobal
```

```bash
createdb ccglobal -O ccglobal
```

#### Configuration

Copy `dev.env` to `.env` and edit it to match your configuration.

```bash
cp dev.env .env
```

#### Start Mage-ai

```bash
docker compose up
```

Navigate to http://localhost:6789