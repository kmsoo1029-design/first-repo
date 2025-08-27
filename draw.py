import numpy as np
import matplotlib.pyplot as plt

def draw_circle(radius, center=(0, 0), color='black', fill=False,
                linewidth=2, figsize=(6, 6), show=True, filepath=None):
	"""
	원 그리기 함수.
	- radius: 원의 반지름 (양수)
	- center: 중심 좌표 (x, y)
	- color: 테두리 / 채움 색상(문자열 또는 색 튜플)
	- fill: True면 내부를 채움
	- linewidth: 테두리 두께
	- figsize: 출력 크기 (inches)
	- show: True면 plt.show()로 화면에 표시
	- filepath: 문자열이면 해당 경로로 이미지 저장 (확장자 권장: .png, .jpg 등)
	"""
	# 입력 간단 검증
	if radius <= 0:
		raise ValueError("radius must be positive")

	theta = np.linspace(0, 2 * np.pi, 400)
	x = center[0] + radius * np.cos(theta)
	y = center[1] + radius * np.sin(theta)

	fig, ax = plt.subplots(figsize=figsize)
	if fill:
		ax.fill(x, y, color=color, alpha=0.6)
	ax.plot(x, y, color=color, linewidth=linewidth)

	# 축 비율 고정 및 보기 영역 설정
	ax.set_aspect('equal', adjustable='box')
	margin = max(radius * 0.1, 0.1)
	ax.set_xlim(center[0] - radius - margin, center[0] + radius + margin)
	ax.set_ylim(center[1] - radius - margin, center[1] + radius + margin)

	ax.axis('off')  # 필요 없으면 변경 가능

	if filepath:
		fig.savefig(filepath, bbox_inches='tight', dpi=150)

	if show:
		plt.show()
	plt.close(fig)

if __name__ == "__main__":
	# 사용 예시: 반지름 2, 중심 (1,1), 파란색 채워진 원을 화면에 표시하고 save.png로 저장
	draw_circle(2, center=(1, 1), color='blue', fill=True, filepath='circle_example.png')