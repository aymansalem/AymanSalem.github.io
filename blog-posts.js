function displayPosts(data) {
  const postsContainer = document.getElementById('blog-posts');
  if (!data.feed.entry) return;

  postsContainer.innerHTML = ''; // clear container first
  const posts = data.feed.entry.slice(0, 3); // latest 3 posts

  posts.forEach(post => {
    const title = post.title.$t;
    const link = post.link.find(l => l.rel === 'alternate').href;
    const publishedDate = new Date(post.published.$t).toLocaleDateString();
    const contentSnippet = post.summary ? post.summary.$t : post.content.$t;
    const excerpt = contentSnippet.replace(/<[^>]*>?/gm, '').substring(0, 100) + '...';

    // Get post image
    let img = '';
    if (post.media$thumbnail) {
      img = post.media$thumbnail.url.replace('/s72-c/', '/s400/'); // higher res
    } else if (post.content && post.content.$t) {
      const imgMatch = post.content.$t.match(/<img.*?src="(.*?)"/);
      img = imgMatch ? imgMatch[1] : 'default-image.jpg'; // fallback image
    }

    postsContainer.innerHTML += `
      <div class="post-card">
        <a href="${link}" target="_blank">
          <img src="${img}" alt="${title}" class="post-image"/>
        </a>
        <a href="${link}" target="_blank" class="post-title">${title}</a>
        <div class="post-meta">${publishedDate} • 3 min read</div>
        <div class="post-excerpt">${excerpt}</div>
      </div>
    `;
  });
}
