FROM node:8.11.1

ENV NODE_ENV=production
ENV HOST 0.0.0.0

RUN mkdir -p /app
COPY . /app
WORKDIR /app
EXPOSE 3000
RUN adduser distrochooser --shell /bin/false --disabled-password --gecos ""
RUN chown distrochooser:distrochooser /app -R
USER distrochooser
RUN npm install
RUN npm run build
CMD ["npm", "start"]