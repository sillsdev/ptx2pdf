# LLM back ends. Each provider turns a prompt string into a reply string.
# To add a new back end: subclass Provider, implement complete(), and register it in _types.
import json
import os
import re
import shutil
import subprocess
import tempfile
import urllib.request


class ProviderError(Exception):
    pass


class Provider:
    def __init__(self, name, cfg):
        self.name = name
        self.cfg = cfg

    def complete(self, prompt):
        raise NotImplementedError


class ClaudeCliProvider(Provider):
    """Runs the Claude Code CLI in print mode (uses your Claude login, no API key).
    Runs from an empty temp directory so project CLAUDE.md files / memory don't leak into the prompt."""

    def complete(self, prompt):
        cmd = self.cfg.get('command', 'claude')
        exe = shutil.which(cmd) or (cmd if os.path.exists(cmd) else None)
        if not exe:
            raise ProviderError("Cannot find '{}'. Put the claude CLI on PATH or set 'command' "
                                "for provider '{}' in localize.toml".format(cmd, self.name))
        args = [exe, '-p', '--output-format', 'text']
        if self.cfg.get('model'):
            args += ['--model', self.cfg['model']]
        args += list(self.cfg.get('extraArgs', []))
        with tempfile.TemporaryDirectory() as td:
            r = subprocess.run(args, input=prompt, capture_output=True, text=True, encoding='utf-8',
                               cwd=td, timeout=self.cfg.get('timeout', 900))
        if r.returncode != 0:
            raise ProviderError("claude exited {}: {}".format(r.returncode, (r.stderr or r.stdout)[:500]))
        return r.stdout


class OpenAiProvider(Provider):
    """Any OpenAI-compatible chat endpoint: LM Studio, Ollama (/v1), llama.cpp server, vLLM, ..."""

    def complete(self, prompt):
        url = self.cfg.get('baseUrl', 'http://localhost:1234/v1').rstrip('/') + '/chat/completions'
        body = {'model': self.cfg.get('model', 'local-model'),
                'messages': [{'role': 'user', 'content': prompt}],
                'temperature': self.cfg.get('temperature', 0.2)}
        if self.cfg.get('maxTokens'):
            body['max_tokens'] = self.cfg['maxTokens']
        req = urllib.request.Request(url, data=json.dumps(body).encode('utf-8'),
                                     headers={'Content-Type': 'application/json',
                                              'Authorization': 'Bearer ' + self.cfg.get('apiKey', 'lm-studio')})
        try:
            with urllib.request.urlopen(req, timeout=self.cfg.get('timeout', 900)) as resp:
                data = json.loads(resp.read().decode('utf-8'))
        except Exception as e:
            raise ProviderError("request to {} failed: {}".format(url, e))
        text = data['choices'][0]['message']['content']
        return re.sub(r'<think>.*?</think>', '', text, flags=re.S)


class MockProvider(Provider):
    """Offline test provider: echoes each English string in brackets. Never use for real output."""

    def complete(self, prompt):
        m = re.search(r'<items>\n(.*?)\n</items>', prompt, re.S)
        items = json.loads(m.group(1))
        return json.dumps([{'id': it['id'], 'msgstr': '[' + it['en'] + ']'} for it in items])


_types = {'claudeCli': ClaudeCliProvider, 'openai': OpenAiProvider, 'mock': MockProvider}


def makeProvider(name, cfg):
    t = cfg.get('type')
    if t not in _types:
        raise ProviderError("Unknown provider type {!r} for '{}' (known: {})".format(t, name, ', '.join(_types)))
    return _types[t](name, cfg)
