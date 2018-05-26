#!/usr/bin/env python3

import boggle

if __name__ == '__main__':
    config = {'ENV': 'development', 'SECRET_KEY': 'dev'}
    app = boggle.create_app(config)
    app.run()
