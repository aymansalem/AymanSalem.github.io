async function loadBloggerPosts() {
  const blogUrl = 'https://4-hoteliers.blogspot.com/feeds/posts/default?alt=json';
  try {
    const response = await fetch(blogUrl);
    const data = await response.json();
    const posts = data.feed.entry.slice(0, 3); // latest 3 posts
    const postsContainer = document.getElementById('blog-posts');
    postsContainer.innerHTML = ''; // clear container first

    posts.forEach(post => {
      const title = post.title.$t;
      const link = post.link.find(l => l.rel === 'alternate').href;
      const publishedDate = new Date(post.published.$t).toLocaleDateString();
      const contentSnippet = post.summary ? post.summary.$t : post.content.$t;
      const excerpt = contentSnippet.substring(0, 100) + '...';

      // Get post image thumbnail
      let img = '';
      if (post.media$thumbnail) {
        img = post.media$thumbnail.url.replace('/s72-c/', '/s150/'); // thumbnail size
      } else if (post.content && post.content.$t) {
        const imgMatch = post.content.$t.match(/<img.*?src="(.*?)"/);
        img = imgMatch ? imgMatch[1] : 'default-thumb.jpg'; // fallback thumbnail
      }

      const postHTML = `
        <div class="post-card">
          <a href="${link}" target="_blank">
            <img src="${img}" alt="${title}" class="post-image"/>
          </a>
          <a href="${link}" target="_blank" class="post-title">${title}</a>
          <div class="post-meta">${publishedDate} • 3 min read</div>
          <div class="post-excerpt">${excerpt}</div>
        </div>
      `;
      postsContainer.innerHTML += postHTML;
    });
  } catch (error) {
    console.error('Error loading posts:', error);
  }
}

document.addEventListener('DOMContentLoaded', loadBloggerPosts);
