//javascript
//
function displayPosts(data) {
  const postsContainer = document.getElementById('blog-posts');
  if (!data.feed.entry) return;

  const posts = data.feed.entry.slice(0, 3); // latest 3

  posts.forEach(post => {
    const title = post.title.$t;
    const link = post.link.find(l => l.rel === 'alternate').href;
    const publishedDate = new Date(post.published.$t).toLocaleDateString();
    const contentSnippet = post.summary ? post.summary.$t : post.content.$t;
    const excerpt = contentSnippet.replace(/<[^>]*>?/gm, '').substring(0, 100) + '...';

    postsContainer.innerHTML += `
      <div class="post-card">
        <a href="${link}" target="_blank" class="post-title">${title}</a>
        <div class="post-meta">${publishedDate} • 3 min read</div>
        <div class="post-excerpt">${excerpt}</div>
      </div>
    `;
  });
}
