# astrago

A simple and fast shortlink service built with Python and FastAPI.

## Overview

Astrago is a simple shortlink service that provides fast URL redirection. The root of the application is a web-based UI that allows you to create, edit, and delete shortlinks.

When a user navigates to a path that is not a defined shortlink, they are presented with a page where they can create a new shortlink for that path.

The entire application is containerized using Docker and managed with Docker Compose for easy setup and deployment. Link management can be handled through the web UI.

## Features

- **Web-Based Management UI:** Create, edit, and delete shortlinks from a user-friendly interface.
- **Fast Redirection:** Built on FastAPI for high performance.
- **SQLite Database:** Lightweight and file-based, perfect for simple applications.
- **Automatic HTTPS:** Automatically prepends `https://` to URLs that are missing a protocol.
- **Interactive CLI:** Easily manage your links from the command line.
- **Dockerized:** Runs in a container for consistent and isolated environments.

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Installation & Running

1. **Clone the repository:**

    ```bash
    git clone https://github.com/emilyastranova/astrago.git
    cd astrago
    ```

2. **Build and run with Docker Compose:**

    ```bash
    docker compose up --build -d
    ```

The service will be running and accessible at [http://localhost:80](http://localhost:80).

## Usage

### Web Interface

Navigate to the root of the application to manage your shortlinks:

```text
http://localhost:80/
```

From here, you can create, edit, and delete shortlinks.

### Web Redirection

To use a shortlink, simply navigate to it in your browser:

```text
http://localhost:80/<your-shortlink>
```

If the shortlink exists, you will be redirected to the destination URL. Otherwise, you will be presented with a page where you can create the shortlink.

### Command-Line Interface (CLI)

You can also manage links by executing commands inside the running container.

## Important Notes

### Firefox Configuration for Single-Word Domains

If you are using this service with a single-word hostname on your internal network (e.g., `http://go/` instead of `http://go.local/`), you may find that Firefox tries to send the query to a search engine instead of resolving the hostname.

To fix this, you need to whitelist your shortlink prefix in Firefox's advanced configuration:

1. Open a new tab and navigate to `about:config`.
2. Accept the warning.
3. In the search bar, type `browser.fixup.domainwhitelist.`
4. You will likely need to create a new boolean entry. To do this, type the full name of your desired setting, e.g., `browser.fixup.domainwhitelist.go`, select `Boolean`, and click the `+` (Add) button.
5. Ensure the value is set to `true`.

Now, when you type `go/your-link`, Firefox will correctly treat `go` as a valid hostname.

### HTTP vs. HTTPS for Internal Use

For internal-only networks, using plain HTTP is often the most straightforward approach. Services like Let's Encrypt cannot issue SSL certificates for single-word domains (as they are not publicly resolvable and you don't own them).

If you require HTTPS, you would need to become your own Certificate Authority (CA), generate your own certificates, and then trust that CA on every device that needs to access the service. This can be a complex process.

## Contributing

Contributions are welcome! Please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
