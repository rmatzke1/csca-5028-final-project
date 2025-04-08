FROM node:18
WORKDIR /home/csca-5028-final-project/applications/web-ui
COPY ../../applications/web-ui/package.json package.json
COPY ../../applications/web-ui/package-lock.json package-lock.json
COPY ../../applications/web-ui/src ./src
RUN npm ci
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
