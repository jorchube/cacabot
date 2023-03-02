
### Prepare the application:

```
make create-container
```


### Run the application:

```
make start-container
```

This requires a `secret.json` file with  telegram bot token.

Also running the application will use a `cacabot.db` and a `cacabot.log` files or will create them if are not found.

### Stop the application:

```
make stop-container
```

### Clean the environment

```
make clean-environment
```
