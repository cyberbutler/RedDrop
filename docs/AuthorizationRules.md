# Authorization Rules
RedDrop offers configurable authorization rules which allow you to specify parameters, headers, and request URIs to match a regular expression in order for RedDrop to process a request. These rules can be defined in a YAML configuration file, or by passing the `-r` CLI argument (once for each rule). 

```bash
python3 reddrop-server.py -r '<Key>=<Regular Expression>' -r '<Key>=<Regular Expression>'
```

A Key can be one of:
- Request Header
- URL
- Request Parameter (GET/POST/PUT)

By Default, no Authorization Rules are set, which means that any request received will be processed.

If a request fails an Authorization Rule, the configured `failure_response` will be returned.

*Be careful, the Keys are case-sensitive, so if you run into an issue where your Authorization Rule is not working, be certain you are matching the case of the expected Key*
