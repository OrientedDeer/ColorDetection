
import circlify
import pandas as pd
import matplotlib.pyplot as plt


fileName = "selfie.pkl"
df = pd.read_pickle(f"data/{fileName}")
df = df.drop("Black")
df = df[df["Count"] > 70_500]
print(df)


# compute circle positions:

circles = circlify.circlify(
    df['Count'].tolist(),
    show_enclosure=False,
    target_enclosure=circlify.Circle(x=0, y=0, r=1)
)

# Create just a figure and only one subplot
fig, ax = plt.subplots(figsize=(10,10))

# Title
ax.set_title(f'Most common colors in {fileName[0:-4]}.jpg')

# Remove axes
ax.axis('off')

# Find axis boundaries
lim = max(
    max(
        abs(circle.x) + circle.r,
        abs(circle.y) + circle.r,
    )
    for circle in circles
)
plt.xlim(-lim, lim)
plt.ylim(-lim, lim)

# list of labels
labels = df.index.tolist()
colors = df["Hex"].tolist()

# matplotlib.RcParams
plt.rcParams['text.color'] = "orangered"
# print circles
for circle, label, color in zip(circles, labels, colors):
    x, y, r = circle
    ax.add_patch(plt.Circle((x, y), r, linewidth=2, facecolor=color))
    plt.annotate(
          label,
          (x, y),
          va='center',
          ha='center',
     )
plt.savefig(f"plots/{fileName[0:-4]}Plot.jpg")
# plt.show()
