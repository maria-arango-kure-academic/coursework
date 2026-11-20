FROM node:22-alpine AS interface
WORKDIR /build
COPY package*.json ./
RUN npm ci
COPY *.jsx *.js *.css index.html ./
COPY public ./public
RUN npm run build

FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt && useradd --uid 10001 --create-home simulation
COPY assets ./assets
COPY *.py *.json ./
COPY --from=interface /build/dist ./dist
USER simulation
EXPOSE 8766
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8766/api/content',timeout=4)"
CMD ["python","server.py","--host","0.0.0.0","--port","8766"]
